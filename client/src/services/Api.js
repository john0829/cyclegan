import axios from 'axios'

export default () => {
  return axios.create({
    baseURL: `http://localhost:3000/`,
    withCredentials: true // 有這行 cookie 才可使用
  })
}