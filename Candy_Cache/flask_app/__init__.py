from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "keep it secret, keep it safe"

bcrypt = Bcrypt(app)

DATABASE = "candy_inventory_db"
