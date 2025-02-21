import { boot } from 'quasar/wrappers'
import axios from 'axios'
import VueSignaturePad from 'vue-signature-pad'

const baseURL = process.env.APP_API_BASE_URL

const api = axios.create({ baseURL })

api.interceptors.request.use(
  config => {
    const token = sessionStorage.getItem('access-token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    if (
      error.response.status === 401 &&
      window.location.pathname !== '/login'
    ) {
      sessionStorage.removeItem('access-token')
      window.location.href = '/login'
    }
    if (error.response.data.detail === 'Token expired') {
      sessionStorage.removeItem('access-token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default boot(({ app }) => {
  app.use(VueSignaturePad)

  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

export { axios, api }
