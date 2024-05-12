import { useSelector, useDispatch } from "react-redux"
import { sendFriendRequest } from "../../features/user-slice/userList"
import { useState } from "react"

export default function UseBlock({user}){

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
            <span>Username: {user.username}</span>
            {
                sent ?
                <span>Sent</span>
                :
                <button onClick={send_friend_request}>Send Friend Request</button>
            }
        </>
    )
}