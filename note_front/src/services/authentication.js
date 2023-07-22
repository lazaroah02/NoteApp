import { GRAPHQL_API } from "@/settings";

function makeFetch(query){
    return fetch(GRAPHQL_API, {
      method:"POST",
      headers: {
        "Content-Type": "application/json",
      },
      body:JSON.stringify({query})
    })  
  }

export function login({username, password}){
    const query = `
        mutation{
            tokenAuth(username:"${username}", password:"${password}"){
            success,
            token,
            user{
                username,
                id
            }
            }
        }
    `
    return makeFetch(query)
    .then(res => res.json())
    .then(data => {return data})
}

export function register({username, email, password1, password2}){
    const query = `
    mutation{
        register(username:"${username}", email:"${email}", password1:"${password1}", password12:"${password2}"){
        success,
        token,
        errors,
        }
    }
    `
    return makeFetch(query)
    .then(res => res.json())
    .then(data => {return data})
}

