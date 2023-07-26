import { makeFetch } from "./base";

export function getNotes({token, orderBy = "-created_at", contains = ""}){
  const query = `{
    notes(orderBy: "${orderBy}", search: "${contains}"){
      edges{
        node{
          id
          title
          content
          createdAt
        }
      }
    }
  }`
  return makeFetch({query: query, token:token})
  .then(res => res.json())
  .then(data => {return data})
}

export function getNote({noteId, token}){
  const query = `{
    note(id: "${noteId}"){
      id
      title
      content
      createdAt
    }
  }`
  return makeFetch({query: query, token: token})
  .then(res => res.json())
  .then(data => {return data})
}

export function createNote({data, token}){
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
  return makeFetch({query: query, token:token})
  .then(res => res.json())
  .then(data => {return data})
}

export function editNote({noteId, token, data}){
  const query = `
  mutation {
    updateNote(id: "${noteId}", title: "${data.title}", content: "${data.content}"){
      note{
        id,
        title,
        content,
      }
    }
  }
`
  return makeFetch({query: query, token:token})
  .then(res => res.json())
  .then(data => {return data})
}

export function deleteNote({noteId, token}){
  const query = `
    mutation {
      deleteNote(id: "${noteId}"){
        message
      }
    }
  `
  return makeFetch({query: query, token:token})
  .then(res => res.json())
  .then(data => {return data})
}

export function bulkDeleteNotes({notesId, token}){
  const query = `
    mutation{
      bulkDeleteNotes(ids: "${notesId}"){
        message
      }
    }
  `
  return makeFetch({query: query, token:token})
  .then(res => res.json())
  .then(data => {return data})
}

