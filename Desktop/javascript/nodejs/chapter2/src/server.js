import express from 'express'
import path, {dirname} from 'path'
import { fileURLToPath } from 'url'
import authRouter from './routes/authroutes.js'
import toDoRouter from './routes/todoRoutes.js'


const app = express()
const PORT = process.env.PORT || 5000 //see if 1 exists in env

//get the path from the URL of the current module
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

//middleware
app.use(express.json())


app.use(express.static(path.join(__dirname, '../public')))//allows  us to send html files

console.log("hello world")

app.get('/',(req,res) =>{
    res.sendFile(path.join(__dirname, "../public" , "index.html"))//sends html
})

app.use('/auth' ,authRouter )
app.use('/todos' , toDoRouter)

app.listen(PORT, ()=>{
    console.log(`server has started on ${PORT}`)
})
