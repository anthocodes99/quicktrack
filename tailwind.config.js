/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
    theme: {
        extend: {
            colors: {
                dark: {
                    100: '#555E62',
                    200: '#4C5457',
                    300: '#42494C',
                    400: '#393F41',
                    500: '#2F3437',
                    600: '#252A2C',
                    700: '#1C1F21',
                    800: '#131516',
                    900: '#090A0B',
                },
            },
        },
    },
    plugins: [],
}
