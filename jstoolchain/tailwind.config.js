module.exports = {
  purge: [
    '../templates/pages/*.html',
    '../templates/users/*.html',
    '../templates/vote/*.html',
    '../templates/*.html',
    '../static/js/custom/*.js',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        'arvo': ['Arvo', 'serif'],
        'lato': ['Lato', 'sans-serif'],
        'raleway': ['Raleway', 'sans-serif']
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
