export function isLoggedIn(){
    let token = localStorage.getItem("jwt")
    if(token === null || token === undefined){
        return false
    }
    else{
        return token
    }
}