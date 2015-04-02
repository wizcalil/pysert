## Introduction ##

_pysert_ (with lowercase ‘p’) is a python script capable of generating random SQL data (INSERTS) from predefined templates .


---


## How it works ##

Let’s suppose you want to in fill the _‘Employees’_ table in your application with 100 random entries . The table has the following columns: (employee\_id, first\_name, last\_name, email, job\_id, salary) .

The first step will be to write the pysert template .  The template is a a simple XML file divided into two sections:
  * A declarative area – Here you define the data sets from which the data is generated ;
  * The template string  - The actual string from which the output is generated .

A possible pysert template for our ‘Employees’ table will look like this:
```
<pysert iterations="20">
	<!--  Declarative area -->
	<dataset name="id" type="Sequence" start="300" increment="1"/>
	<dataset name="fname" type="PersonalName" firstname="True" lastname="False"/>
	<dataset name="lname" type="PersonalName" firstname="False" lastname="True"/>
	<dataset name="jobid" type="RandomNumber" floating="False" min="100" max="200"/>
	<dataset name="salary" type="RandomNumber" floating="False" min="1000" max="15000"/>
	<!--  Actual template to be converted -->
	<template>
INSERT INTO EMPLOYEES
	(EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL, JOB_ID, SALARY)
VALUES 
	(#{id}, '#{fname}', '#{lname}', '#{fname}_#{lname}@domain.com', #{jobid}, 
	#{salary})
	</template>
 </pysert>
```

Once the template is ready you can use the script to generate the results . In it’s current form the script works perfectly with both python 2.7.x and python 3.2.x series:

```
PS D:\workspace\python\pySert\src> python .\pysert.py --input .\tmpl.xml
```

The generated output will be printed directly to stdout (unless you specify an –output FILE):

```
INSERT INTO EMPLOYEES
        (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL, JOB_ID, SALARY)
VALUES
        (310, 'Mikolaj', 'Botev', 'Mikolaj_Botev@domain.com', 121,
        5755)


INSERT INTO EMPLOYEES
        (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL, JOB_ID, SALARY)
VALUES
        (311, 'Leah', 'Hancock', 'Leah_Hancock@domain.com', 195,
        3521)


INSERT INTO EMPLOYEES
        (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL, JOB_ID, SALARY)
VALUES
        (312, 'Emma', 'Varchol', 'Emma_Varchol@domain.com', 187,
        5445)
```

(more entries ...)

---


## Examples on how to use data sets ##

**LoremIpsum**
```
<dataset name="name" type="LoremIpsum" length="100"/>
```
Generates 100 characters long "LoremIpsum" text .

**PersonalName**
```
<dataset name="name" type="PersonalName" firstname="True" lastname="False"/>
```
Generates a random person first name for every iteration .

**RandomNumber**
```
<dataset name="name" type="RandomNumber" floating="False" min="1000" max="15000"/>
```
Generates a random integer number between [1000, 15000)

**Sequence**
```
<dataset name="id" type="Sequence" start="300" increment="1"/>
```
Generates numbers in a sequence . The first number is 300, increment is 1 .
