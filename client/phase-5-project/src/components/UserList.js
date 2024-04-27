import { useDispatch, useSelector } from "react-redux"
import { fetchUserList } from "../features/user/userList"
import { useState } from "react"

export default function UserList(){

    const userList = useSelector((store) => store.userList.value)
    const dispatch = useDispatch()
    
    window.addEventListener("beforeunload", () => {
        fetch('/onRefresh')
        .then((r) => {
            if(r.ok) return r.json()
            else if(r.status === 404) throw new Error("Error, could not be sent")
        })
        .then((r) => console.log(r))
        .catch((err) => console.log(err))
    })

    console.log(userList)

    return(
        <>
            <button onClick={() => dispatch(fetchUserList())}>Show Users</button>
            {
                userList.length > 0 ?
                userList.map((user) => {
                    return <>{user.first_name}</>
                })
                :
                null
            }
        </>
    )
}