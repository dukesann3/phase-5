import { useSelector, useDispatch } from "react-redux"
import { increment, decrement, incrementByAmount, selectAddedString} from "../features/test_slice_1/test_slice_1"
import { fetchAllUsers } from "../features/test_slice_2/test_slice_2"

function Tester(){

    const count = useSelector((state) => state.test_counter.value)
    const users = useSelector((state) => state.test_thunk.value)
    const countWithString = selectAddedString(count)

    const dispatch = useDispatch()

    const incrementByAmountSubmitter = (e) => {
        e.preventDefault()
        const userInputValue = parseInt(e.target.querySelector(".increment_by_amount").value)
        dispatch(incrementByAmount(userInputValue))
    }

    const getAllUsers = (e) => {
        e.preventDefault()
        dispatch(fetchAllUsers())
    }

    return(
        <>
            <div>
                <p>This is Tester</p>
                <span>{count}</span>
                <p>Counter With String</p>
                <span>{countWithString}</span>
                <div>
                    <button onClick={() => dispatch(increment())}>+</button>
                    <button onClick={() => dispatch(decrement())}>-</button>
                </div>
                <form onSubmit={incrementByAmountSubmitter}>
                    <span>By Amount</span>
                    <input className="increment_by_amount" type="number"/>
                    <input type="submit"/>
                </form>
            </div>
            <div>
                <h3>Fetch Button</h3>
                <form onSubmit={getAllUsers}>
                    <input type="submit" value="press to fetch" />
                    {
                        users ? 
                        <>
                            {users.map((user) => {
                                return <p key={user.id}>{user.name}</p>
                            })}
                        </>
                        :
                        null
                    }
                </form>
            </div>
        </>
    )
}

export default Tester;