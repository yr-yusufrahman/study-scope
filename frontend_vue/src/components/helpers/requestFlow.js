import axios from "axios";
import refresh from "./refresh";

// Request flow for getting courses and refreshing token
export default function makeRequest(requestCall) {
    let success = requestCall()
    if (!success) {

        // Refresh token
        let refreshed = refresh()
        if (refreshed) {
            success = requestCall()
        }
        else {
            // Failed to refresh token
            success = false
        }
    }

    return success
} 

async function makeRequestOld(requestCall) {
    let success = false

    try {
        success = await requestCall()
    } catch (error) {
        // refresh token
        let refreshed = await refresh()
        if (refreshed) {
            success = await requestCall()
        } else {
            // Failed to refresh token
            success = false
        }
    }
    return success
} 