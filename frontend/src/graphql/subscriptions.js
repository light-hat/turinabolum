// src/graphql/subscriptions.js
import { gql } from '@apollo/client';

export const COUNT_SUBSCRIPTION = gql`
  subscription {
    countSeconds
  }
`;
