import { useSelector, useDispatch } from "react-redux"
import { sendFriendRequest } from "../../features/user-slice/userList"
import { useState } from "react"
import { NavLink } from "react-router-dom"
import {ListContent, Image, ListHeader, ListDescription, Button} from "semantic-ui-react"
import 'semantic-ui-css/semantic.min.css'

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
            <Image avatar src={user._image_src}/>
            <ListContent>
                <ListHeader>            
                    <NavLink to={`/user/${user.id}/profile`}>
                        <span>Username: {user.username}</span>
                    </NavLink>
                </ListHeader>
                <ListDescription>
                {
                    sent || isPending?
                    <span>Friend Request Sent</span>
                    :
                    isFriend ?
                    <span>Friend</span>
                    :
                    <Button onClick={send_friend_request}>Send Friend Request</Button>
                }
                </ListDescription>
            </ListContent>
        </>
    )
}