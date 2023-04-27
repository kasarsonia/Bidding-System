const express = require('express');
const oracledb = require('oracledb');
oracledb.outFormat = oracledb.OUT_FORMAT_OBJECT;

const app = express();
const port = 3000;

app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/bid.html');
});

oracledb.getConnection({
  user: 'system',
  password: 'system',
  connectString: '//localhost:1521/xe'
})
.then(conn => {
  console.log('Connected to Oracle Database');

  app.post('/insert', (req, res) => {
    const name = req.body.name;
    const email = req.body.email;
    const amount = req.body.amount;

    const sql = 'INSERT INTO people (name, email, amount) VALUES (:name, :email, :amount)';
    const bindParams = { name, email, amount };

    conn.execute(sql, bindParams)
    .then(result => {
      console.log('Rows inserted: ' + result.rowsAffected);
      res.send('Bid successfully submitted');
    })
    .catch(err => {
      console.error(err);
      res.status(500).send('Error inserting bid into database');
    })
    .finally(() => {
      conn.release();
    });
  });

  app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
  });
})
.catch(err => {
  console.error(err);
});
