import asyncio
import os
import tempfile
from typing import Dict
from uuid import UUID, uuid4

from fastapi import BackgroundTasks, FastAPI

from .config import Config
from .models import ProcessingRequest, TaskStatus
from .utils import download_from_s3, run_plaso_command

app = FastAPI(title="Plaso Processing Service")
tasks: Dict[UUID, TaskStatus] = {}


@app.post("/process", response_model=dict)
async def process_dump(request: ProcessingRequest, background_tasks: BackgroundTasks):
    task_id = uuid4()
    tasks[task_id] = TaskStatus(task_id=task_id, status="pending", progress=0.0)

    background_tasks.add_task(
        process_dump_task,
        task_id=task_id,
        dump_id=request.dump_id,
        s3_url=request.s3_url,
    )

    return {"task_id": task_id, "message": "Processing started"}


@app.get("/status/{task_id}", response_model=TaskStatus)
async def get_status(task_id: UUID):
    return tasks.get(task_id, {"status": "not_found"})


async def process_dump_task(task_id: UUID, dump_id: UUID, s3_url: str):
    task = tasks[task_id]
    task.status = "processing"
    task.progress = 0.1

    with tempfile.TemporaryDirectory(dir=Config.TEMP_DIR) as tmp_dir:
        try:
            # Скачивание дампа
            dump_path = os.path.join(tmp_dir, f"{dump_id}.dump")
            await download_from_s3(s3_url, dump_path)
            task.progress = 0.3

            # Обработка log2timeline
            storage_file = os.path.join(tmp_dir, "storage.plaso")
            log2timeline_cmd = [
                "log2timeline.py",
                "--status_view",
                "none",
                "--workers",
                str(Config.MAX_WORKERS),
                "--storage_file",
                storage_file,
                dump_path,
            ]
            log_output = run_plaso_command(log2timeline_cmd)
            task.progress = 0.7

            # Экспорт в OpenSearch через psort
            psort_cmd = [
                "psort.py",
                "--status_view",
                "none",
                "-o",
                "opensearch",
                "--server",
                Config.OPENSEARCH_HOST,
                "--index-name",
                f"{Config.OPENSEARCH_INDEX_PREFIX}-{dump_id}",
                storage_file,
            ]
            psort_output = run_plaso_command(psort_cmd)
            task.progress = 1.0
            task.status = "completed"
            task.logs = (
                f"Log2timeline output:\n{log_output}\n\nPsort output:\n{psort_output}"
            )

        except Exception as e:
            task.status = "error"
            task.logs = str(e)
