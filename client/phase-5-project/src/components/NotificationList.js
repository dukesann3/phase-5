import { useSelector } from "react-redux"
import NotificationBlock from "./NotificationBlock"

export default function NotificationList(){
    const userInfo = useSelector((store) => store.loggedInUser)
    console.log(userInfo)
    return(
        <>
            <span>Notification List</span>
            {   Object.keys(userInfo.value).length !== 0 ?
                userInfo.value.notifications.map((notification) => {
                    //try to distinguish between friend request notification and post like/ comment like notification
                    return <NotificationBlock key={notification.id} notification={notification}/>
                })
                :
                null
            }
        </>
    )
}