
import { makeFetch } from "./base";

export function getUserProfile({token}){
    const query = `{
        me{
            username
        }
    }`

    return makeFetch({query:query, token:token})
    .then(res => res.json())
    .then(data => {return data})
}