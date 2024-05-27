import { useDispatch, useSelector } from "react-redux"
import { fetchUserList, unLoadErrorMsg } from "../../features/user-slice/userList"
import { useParams, NavLink } from "react-router-dom"
import { useEffect } from "react"
import UserBlock from "./UserBlock"
import { fetchUser } from "../../features/user-slice/user"

export default function UserList(){

    const userList = useSelector((store) => store.userList)
    const dispatch = useDispatch()
    let { user_id } = useParams()

    console.log(userList.value)

    useEffect(() => {
        if(userList.errorMessage !== ""){
            onErrorMsg(userList.errorMessage)
        }
    },[userList.errorMessage])
    
    window.addEventListener("beforeunload", (e) => {
        e.preventDefault()
        fetch('/onrefresh', {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 401) throw new Error("Error, could not be sent")
            throw new Error("Network Error")
        })
        .then((r) => console.log(r))
        .catch((err) => console.log(err))
    })

    function onErrorMsg(resp){
        const errorMsgDOM = document.querySelector(".userlist-error-msg")
        errorMsgDOM.textContent = `${resp}`
        setTimeout(() => {
            errorMsgDOM.textContent = ""
            dispatch(unLoadErrorMsg())
        }, 3000)
    }

    return(
        <>
            <input 
            type="text"
            placeholder="search username"
            onChange={(e) => dispatch(fetchUserList({search_query: e.target.value}))}
            />
            
            {
                userList.value.length > 0 ?
                <>
                    {userList.value.map((user) => {
                        return (
                            <UserBlock key={`${user.id}_${user.username}`} user={user}/>
                        )
                    })}
                </>
                :
                null
            }
            <span className='userlist-error-msg'></span>
        </>
    )
}