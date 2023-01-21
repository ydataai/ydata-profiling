module.exports = {
    extends: ['@commitlint/config-conventional'],
    ignores: [(message) => message.includes('Merge branch') || message.includes('[skip ci]')],
    rules: {
        'body-max-line-length': [2, 'always', 120],
        'footer-max-line-length': [2, 'always', 120],
    },
};
