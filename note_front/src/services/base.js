import { GRAPHQL_API } from "@/settings";

export function makeFetch({query, token}){
    return fetch(GRAPHQL_API, {
      method:"POST",
      headers: {
        "Authorization": `JWT ${token}`,
        "Content-Type": "application/json",
      },
      body:JSON.stringify({query})
    })  
  }