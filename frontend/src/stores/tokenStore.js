import { ref} from 'vue'
import { defineStore } from 'pinia'

export const useTokenStore = defineStore('token', () => {

  const token = ref(null)

  function isAuthenticated(){
    if(token.value==null){
      return false
    }
    else{
      return true
    }
  }

  const setToken = (newToken) => {
    token.value = newToken
  }

  const removeToken = () => {
    token.value = null
  }

  return {
    token,
    isAuthenticated,
    setToken,
    removeToken,
  }
})
