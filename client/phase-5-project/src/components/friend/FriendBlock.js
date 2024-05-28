// import 'semantic-ui-css/semantic.min.css'
import { CardContent, CardHeader, CardMeta } from 'semantic-ui-react'
import "../../CSS/friendblock.css"

function FriendBlock({friend}){

    const {first_name, last_name, username, status} = friend

    return(
        <CardContent className="friend-block-content">
            <CardMeta>{status}</CardMeta>
            <div className="friend-block-info-container">
                <CardHeader>USERNAME: {username}</CardHeader>
                <CardHeader>FIRST: {first_name}</CardHeader>
                <CardHeader>LAST: {last_name}</CardHeader>
            </div>
        </CardContent>
    )
}

export default FriendBlock