
export function updatedAtComparator(a,b){

    const aDate = new Date(a["updated_at"])
    const bDate = new Date(b["updated_at"])
    if(aDate > bDate) return -1
    else if(aDate < bDate) return 1
    return 0

}