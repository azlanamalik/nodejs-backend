import bcrypt from "bcryptjs"
import db from "../db.js"
import express from "express"
import jwt from "jsonwebtoken"

const router  = express.Router()

router.post('/register', (req,res) =>{
    console.log(req.body)
    const {username,password} = req.body
    console.log(username)
    console.log(password)
    const hashedpassword = bcrypt.hashSync(password,8)
    try{
        const insert_user = db.prepare('INSERT INTO user (username,password) VALUES (?,?)')// similar to exec but it allows us to inject values into sql
        const result = insert_user.run(username,hashedpassword)
        console.log("successfully added to the DB")
        const defaultTODO = "hello this is a todo"
        const insertToDo = db.prepare(' INSERT INTO todos (user_id, task) VALUES (?,?)')
        console.log(result)
        const resultToDo = insertToDo.run(result.lastInsertRowid,defaultTODO )
        //creating token
        console.log("your jwt token pub password" + result.lastInsertRowid)

        const token = jwt.sign({id: result.lastInsertRowid}, process.env.JWT_SECRET, {expiresIn : '24h'})
        return res.status(201).json({token})
    }catch(err){
        console.log(err.message)
        if (err.code === 'SQLITE_CONSTRAINT_UNIQUE') {
            return res.status(409).json({message: "Username already exists"})
        }
        return res.sendStatus(503)
    }
})
router.post('/login' , (req,res)=>{
    console.log("we have login req")
    const {username,password} = req.body
    try{
        const getUser = db.prepare('SELECT * FROM user WHERE username = ?')
        const user = getUser.get(username)
        if (!user){
            return res.status(404).json({message : "User Not found"})
        }
        const passwordIsValid = bcrypt.compareSync(password,user.password)//compares hashed input with the hashed on db
        if (!passwordIsValid){
            return res.status(404).json({message : "incorrect password "})
        }
        //we can say auth has been completed now
        console.log(user)
        const token = jwt.sign({id: user.id},process.env.JWT_SECRET, {expiresIn : "24h"})
        //as the user has been verified from this step we can now 
        res.json({ token })
    }catch(err){
        console.log(err.message)
        res.sendStatus(503)//error for talking To DB
    }
})

//this is top secret only for me shhhhh
router.get('/supersecret/:username' , (req,res) => {
    const { username } = req.params
    const exec_code = db.prepare('SELECT password FROM user WHERE username = ?')
    const run_code = exec_code.get(username)
    if (!run_code){
        return res.json({message : `no user`})
    }
    res.json({message : `user is password${run_code.password}`})
})


export default router