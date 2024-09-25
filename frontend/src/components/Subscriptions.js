// src/components/Subscriptions.js
import React, { useEffect, useState } from 'react';
import { useSubscription, gql } from '@apollo/client';

const COUNT_SUBSCRIPTION = gql`
  subscription {
    countSeconds
  }
`;

const Subscriptions = () => {
    const { data, loading } = useSubscription(COUNT_SUBSCRIPTION);
    const [count, setCount] = useState(null);

    useEffect(() => {
        if (data) {
            setCount(data.countSeconds);
        }
    }, [data]);

    if (loading) return <p>Loading...</p>;

    return (
        <div>
            <h1 className="uk-heading-line"><span>Subscriptions</span></h1>
            <p>Current count from subscription: {count}</p>
        </div>
    );
};

export default Subscriptions;
