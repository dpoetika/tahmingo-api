import axios from "axios";
import { ENV } from "../config/env.js";

export async function get_live_matches() {
    const { data } = await axios.get(`${ENV.MATCHES}`);
    const events = data.data.events

    const all_matches = []

    for (let i = 0; i < events.length; i++) {
        if (events[i]["s"] === 1) {
            let match_details = {}
            match_details["id"] = events[i]["i"]

            let { data } = await axios.get(`${ENV.MATCH_DETAIL}/${match_details["id"]}`);
            const match = data.data

            match_details["title"] = `${match["hn"]} - ${match["an"]}`
            match_details["time"] = new Date(match["d"] * 1000).toLocaleString()

            match_details["min"] = match["sc"]["min"]

            match_details["home_first_half"] = match["sc"]["ht"]["ht"]
            match_details["away_first_half"] = match["sc"]["at"]["ht"]

            match_details["home_total"] = match["sc"]["ht"]["c"]
            match_details["away_total"] = match["sc"]["at"]["c"]

            //const odds = []
            let ODDS = await axios.get(`${ENV.ODDS_URI}/${match_details["id"]}`);
            const odds_data = ODDS.data
            console.log(`${ENV.ODDS_URI}/${match_details["id"]}`)

            const all_odds = odds_data.marketGroups[0].odds
            
            const odds = all_odds.map(element => {
                return {"odd_title":element.mrn,"odd_name":element.n,"odd_value":element.val}
            });
            console.log(odds)
            match_details["odds"] = odds
            all_matches.push(match_details)
            
        }
    }

    return { message: "succes", "data": all_matches };
}