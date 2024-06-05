import { useDispatch, useSelector } from "react-redux"
import { fetchUserList, unLoadErrorMsg } from "../../features/user-slice/userList"
import { useEffect } from "react"
import UserBlock from "./UserBlock"
import { List, ListItem } from "semantic-ui-react"
import 'semantic-ui-css/semantic.min.css'
import '../../CSS/userlist.css'

export default function UserList(){

    const userList = useSelector((store) => store.userList)
    const dispatch = useDispatch()

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
        <div className="grid-container-userlist">
            <div className="search-container userlist-grid-item">
                <input 
                type="text"
                placeholder="search username"
                onChange={(e) => dispatch(fetchUserList({search_query: e.target.value}))}
                className="search-input"
                />
            </div>
            
            {
                userList.value.length > 0 ?
                <List className="userList-grid-item userList">
                    {userList.value.map((user) => {
                        return (
                            <ListItem key={`${user.id}_${user.username}`}><UserBlock key={`${user.id}_${user.username}`} user={user}/></ListItem>
                        )
                    })}
                </List>
                :
                null
            }
            <span className='userlist-error-msg'></span>
        </div>
    )
}