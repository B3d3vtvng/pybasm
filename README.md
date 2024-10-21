#Transpiler from Python to C

##Content

- Introduction
- Features
- Use Cases
- Currently developed parts
- Contributing
- Build process


##Introduction

This Project has been a dream of mine for about half a year now. Do not take this project and especially the code too serious as this is nothing but a toy project. I would be happy about tips for absolutely everything because this is my first real big project and I am the complete opposite of experienced.


##Features

Features will be supported when I have finished the Compiler include:

- Basic data types (int, str, bool, float, lists)
- Basic arithmetic operations (add, subtract, multiply, divide)
- Basic logical operations (and, op, ==, <, ...)
- Basic control flow structures (if, elif, else, while, for, ...)
- Variables
- Functions
- Basic I/O operations (read, print)
- Basic build-in functions (len(), type casting, ...)

Possible features in the future could be:

- A Python-like pass keyword
- A Python-like break keyword
- More advanced data types (tuple, dict, ...)

I am not planning an implementing classes.


##Use Cases

Possible use cases could be optiming simple but performance-critical functions by compiling them to C and including them as C functions into an existing Python file or just as a fun toy to play around with. If anyone has any other ideas on what this could be useful for, just make an issue and I will include it here.


##Currently developed parts

I have already implemented and tested the Lexer and I am currently working on testing and debugging the Parser. When I get sick of coding 5 hours of Python everyday, I usually work on some header files implementing helper functions and structs to be included in the finished output file for easier work with the code generation process.


##Contributing

As I mentioned, I am kind of unexperienced on this topic so I will refrain from demanding a certain coding style or good documentation for pull requests. Please just make sure that your code actually works and i will probably accept it :)


##Build process

I am proud to say that the python part of this project has no dependencies. No extern libraries are used. For the C part of the project, a basic C compiler shoud do the job, in general, just cloning the project and running the main file with the file to compile being the first commandline argument should be enough. I will probably extend this section when I get to directly compiling a python file to a binary.
