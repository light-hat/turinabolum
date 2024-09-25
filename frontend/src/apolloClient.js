import { ApolloClient, InMemoryCache, HttpLink, split, ApolloProvider } from '@apollo/client'; // Добавили ApolloProvider
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';
import { getMainDefinition } from '@apollo/client/utilities';

const httpLink = new HttpLink({
    uri: 'http://localhost/graphql',  // Адрес GraphQL сервера
});

const wsLink = new GraphQLWsLink(createClient({
    url: 'ws://localhost/ws/',  // WebSocket для подписок
}));

const splitLink = split(
    ({ query }) => {
        const definition = getMainDefinition(query);
        return (
        definition.kind === 'OperationDefinition' &&
        definition.operation === 'subscription'
        );
    },
    wsLink,
    httpLink
);

const client = new ApolloClient({
    link: splitLink,
    cache: new InMemoryCache(),
});

export const ApolloWrapper = ({ children }) => (
    <ApolloProvider client={client}>
        {children}
    </ApolloProvider>
);
