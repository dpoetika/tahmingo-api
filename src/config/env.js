import dotenv from "dotenv";

dotenv.config();

export const ENV = {
    PORT: process.env.PORT,
    NODE_ENV: process.env.NODE_ENV,
    MATCH_DETAIL: process.env.MATCH_DETAIL,
    MATCHES: process.env.MATCHES,
    ODDS_URI: process.env.ODDS_URI,
};