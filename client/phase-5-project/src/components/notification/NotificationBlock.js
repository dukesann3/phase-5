import { useDispatch } from "react-redux"
import { deleteNotification, respondToFriendRequest, respondToFriendRequestAndGetPost } from "../../features/user-slice/user"
import { CardContent, CardHeader, Button, Card, CardDescription} from "semantic-ui-react"   
import 'semantic-ui-css/semantic.min.css'

export default function NotificationBlock({notification}){

    const notification_mapper = {
        friend_request_notifications: "Friend Request",
        post_like_notifications: "Post Like",
        comment_notifications: "Comment",
        comment_like_notifications: "Comment Like"
    }

    const notification_type = (imported_notification_type) => {
        const notification = notification_mapper[imported_notification_type]
        if(notification) return notification
        else{
            return false
        }
    }

    const dispatch = useDispatch()

    const noteInfoToDelete = {
        id: notification.value.id,
        type: notification.type
    }

    //play around with this function and if it works, replace it with redux

    const onFriendRequestResponse = (response) => {
        const friendship_id = notification.value.friendship_id
        dispatch(respondToFriendRequestAndGetPost(friendship_id, response))
    }

    return(
        <Card>
            <CardContent>
                <CardHeader>{notification_type(notification.type)}</CardHeader>
                <CardDescription>{notification.value.text}</CardDescription>
            </CardContent>
            {
                notification.type === "friend_request_notifications"?
                <div className="ui two buttons">
                    <Button basic color="green" onClick={() => onFriendRequestResponse("accepted")}>Accept</Button>
                    <Button basic color="red" onClick={() => onFriendRequestResponse("rejected")}>Reject</Button>
                </div>
                :
                <Button onClick={() => dispatch(deleteNotification(noteInfoToDelete))}>DELETE</Button>
            }
        </Card>
    )
}