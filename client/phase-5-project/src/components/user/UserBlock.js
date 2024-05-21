import { useSelector, useDispatch } from "react-redux"
import { sendFriendRequest } from "../../features/user-slice/userList"
import { useState } from "react"
import { NavLink } from "react-router-dom"

export default function UseBlock({user}){

    const {isFriend, isPending} = user
    const loggedInUser = useSelector((store) => store.user.value)
    const dispatch = useDispatch()
    const [sent, setSent] = useState(false)

    function send_friend_request(){
        dispatch(sendFriendRequest({
            sender_id: loggedInUser.id,
            reciever_id: user.id
        }))
        setSent(true)
    }

    return(
        <>
            <span>First Name: {user.first_name}</span>
            <span>Last Name: {user.last_name}</span>
            <NavLink to={`/user/${user.id}/profile`}>
                <span>Username: {user.username}</span>
            </NavLink>
            {
                sent || isPending?
                <span>Sent</span>
                :
                isFriend ?
                <span>is Friend</span>
                :
                <button onClick={send_friend_request}>Send Friend Request</button>

            }
        </>
    )
}