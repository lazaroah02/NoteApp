import { createStore } from 'vuex'
import {getUserProfile} from './services/userProfile'

export const store = createStore({
  state () {
    return {
      infoUser: {username:null, token:null}
    }
  },
  mutations: {
    setInfoUser(state, {username, token}){
        state.infoUser.username = username
        state.infoUser.token = token
    },
    fetchInfoUser(state, {token}){
      getUserProfile({token:token})
      .then(data => {
        state.infoUser.username = data.data.me.username
        state.infoUser.token = token
      })
    }
  },
  actions: {
  
  }
})