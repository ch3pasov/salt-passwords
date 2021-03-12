# salt-passwords
some code for "Зачем солить почту?" video.

### Requirements.
1. Python3
2. Numpy\Pandas

## preparation.
1. Convert __files/dont_touch/top-200_raw__ to machine-readble .csv:
```
$ python3 1_raw_top-200_to_csv.py
```

2. Generate __realistic__ accounts database:
```
$ python3 2_generate_db.py --verbose <db_size>
```
Caution: it may be if you want large database.

Run script with __--salted__ flag, if you want salted database.
```
$ python3 2_generate_db.py --verbose --salted <db_size>
```
or
```
$ python3 2_generate_db.py -sv <db_size>
```

## repeat video plot.
1. Make hash values __frequency analysis__ of salted\unsalted database:
```
$ python3 a_equivalence_class.py <db_size>
```
Add __-s__ flag, if your database is salted.
If database is unsalted, script will get most popular hash and try to compare it with '12345' hash.

2. __Unsalted__ database __dictionary attack__:
```
$ python3 b_top-200_hack.py <db_size>
```
Unsalted database only.

3. __Salted__ database __dictionary attack__:
```
$ python3 c_salted_hack_try.py <db_size>
```
Salted database only.

4. Attack __result analysis__:
```
$ python3 d_hack_results.py -s <db_size>
```
Use __-s__ flag if salted database.

5. __VIP dictionary attack__:
```
$ python3 e_salted_aimed_hack.py
```

## some stuff.
1. __Get sha-256 hash__ of string:
```
$ python3 hash.py -v <string>
```
