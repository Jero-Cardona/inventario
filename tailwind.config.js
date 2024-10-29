/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/src/**/*.css',
    './app/**/*.py'
  ],
  theme: { 
    fontFamily: {
      rale: ['Raleway'],
      rubi: ['Rubik']
    },
    extend: {
      colors: {
        Andes: '#13A438',
        Nac: '#084F21',
        delete: '#084F21',
        info:{
          100: '#5B5C5C',
          200: '#DDDDDD'
        }
      }
    },
  },
  plugins: [
    require('flowbite/plugin')({
        datatables: true,
    }),
    // ... other plugins
  ]
}