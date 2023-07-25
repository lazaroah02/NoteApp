import { makeFetch } from "./base";

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
    return makeFetch({query:query})
    .then(res => res.json())
    .then(data => {return data})
}

export function register({username, email, password1, password2}){
    const query = `
    mutation{
        register(username:"${username}", email:"${email}", password1:"${password1}", password2:"${password2}"){
        success,
        token,
        errors,
        }
    }
    `
    return makeFetch({query:query})
    .then(res => res.json())
    .then(data => {return data})
}


