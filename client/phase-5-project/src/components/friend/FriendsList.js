import { useDispatch, useSelector } from "react-redux"
import { getFriends, unfriend } from "../../features/friend-slice/friend"
import { useEffect } from "react"
import { NavLink } from "react-router-dom"
import FriendBlock from "./FriendBlock"

function FriendsList(){

    const dispatch = useDispatch()
    const friends = useSelector((state) => state.friends)

    useEffect(() => {
        dispatch(getFriends())
    },[])

    return(
        <>
            <span>Friends List</span>
            {
                Object.keys(friends.value).length !== 0 ?

                friends.value.map((f) => {
                    return (
                        <>
                            <NavLink to={`/user/${f.id}/profile`}>
                                <FriendBlock key={f.id} friend={f} status={f.status}/>
                            </NavLink>
                            {f.status !== "pending" ? <button onClick={() => dispatch(unfriend(f.id))}>unfriend</button> : null}
                        </>
                    )
                })

                :
                null
            }
        </>
    )
}

export default FriendsList