module.exports = {
    extends: ['plugin:vue/essential', 'eslint:recommended'],
    parserOptions: {
        ecmaVersion: 2020,
    },
    ignorePatterns: ['*.json'],
    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    },
}
