import { makeFetch } from "./base";

export function getNotes({token}){
  const query = `{
    notes{
      edges{
        node{
          id
          title
          content
        }
      }
    }
  }`
  return makeFetch({query: query, token:token})
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
  return makeFetch({query: query})
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
  return makeFetch({query: query})
  .then(res => {
    if(res.status === 200){
      res.json()
    }else{
      throw new Error("")
    }
  })
  .then(data => {return data})
}

export function editNote({noteId, token, data}){
  const query = `
  mutation {
    editNote(id: ${noteId}, title: "${data.title}", content: "${data.content}"){
      success,
      note{
        id,
        title,
        content,
      }
    }
  }
`
  return makeFetch({query: query, token:token})
  .then(res => {
    if(res.status === 200){
      return "Nota Editada correctamente"
    }else{
      return "Error al editar la nota"
    }
    })
}

export function deleteNote({noteId, token}){
  const query = `
    mutation {
      deleteNote(id: ${noteId}){
        message
      }
    }
  `
  return makeFetch({query: query, token:token})
  .then(res => {
    if(res.status === 200){
      return "Nota borrada correctamente"
    }else{
      return "Error al eliminar la nota"
    }
    })
}

