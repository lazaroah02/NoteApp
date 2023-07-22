import axios from "axios";
import { GRAPHQL_API } from "@/settings";

function makeFetch(query){
  return fetch(GRAPHQL_API, {
    method:"POST",
    headers: {
      "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Inl1bGkiLCJleHAiOjE2OTAwNTQzMTMsIm9yaWdJYXQiOjE2OTAwNTQwMTN9.PICHA7reVV9r8XBqLtuT9Xy7vsR2LPJxI4uYIucMP_I",
      "Content-Type": "application/json",
    },
    body:JSON.stringify({query})
  })  
}

export function getNotes(){
  const query = `{
    notes{
      id
      title
      content
    }
  }`
  return makeFetch(query)
  .then(res => res.json())
  .then(data => {return data})
}

export function getNote(noteId){
  const query = `{
    note(id: ${noteId}){
      id
      title
      content
    }
  }`
  return makeFetch(query)
  .then(res => res.json())
  .then(data => {return data})
}

export function createNote(data){
  const query = `
    mutation {
      createNote(title:"${data.title}", content:"${data.content}"){
        note{
          id
          title
          content
        }
      }
    }
    
    `
  return makeFetch(query)
  .then(res => {
    if(res.status === 200){
      res.json()
    }else{
      throw new Error("")
    }
  })
  .then(data => {return data})
}

export function editNote(noteId, data){
    return axios.put(`${GRAPHQL_API}${noteId}/`, data)
    .then(res => {return res})
}

export function deleteNote(noteId){
  const query = `
    mutation {
      deleteNote(id: ${noteId}){
        message
      }
    }
  `
  return makeFetch(query)
  .then(res => {
    if(res.status === 200){
      return "Nota borrada correctamente"
    }else{
      return "Error al eliminar la nota"
    }
    })
}

