import express from "express"
import { get_live_matches } from "../controllers/matches.controller.js";

const matchRouter = express.Router()

matchRouter.get("/",async(req,res)=>{res.send(await get_live_matches());})

export default matchRouter