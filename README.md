# Transpiler from Python to C

## Content

- Introduction
- Features
- Use Cases
- Currently developed parts
- Contributing
- Build process


## Introduction

This Project has been a dream of mine for about half a year now. Do not take this project and especially the code too serious as this is nothing but a toy project. I would be happy about tips for absolutely everything because this is my first real big project and I am the complete opposite of experienced.


## Features

Features that will be supported when I have finished the Transpiler include:

- Variables with basic data types (int, str, bool, float, lists)
- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Basic logical operations (and, or, ==, <, ...)
- Basic control flow structures (if, elif, else, while, for, ...)
- Functions
- Basic I/O operations (read, print)
- Basic built-in functions (len(), type casting, ...)

Possible features in the future could be:

- A Python-like pass keyword
- A Python-like break keyword
- More advanced data types (tuple, dict, ...)

I am not planning on implementing OOP features.


## Use Cases

Possible use cases could be optimising simple but performance-critical functions by compiling them to C and including them as C functions into an existing Python file. Or just as a fun toy to play around with. If anyone has any other ideas on what this could be useful for, just make an issue and I will include it here.


## Currently developed parts

I have already implemented and tested the Lexer and I am currently working on testing and debugging the Parser. When I get sick of coding 5 hours of Python everyday, I usually work on some header files implementing helper functions and structs to be included in the finished output file for easier work with the code generation process.


## Contributing

This Repository is currently not open for Contributing as it is a school project of mine and it will be plagiarism if I include any work that has not been done by myself. 
This is going to change in Summer 2025 when I will have submitted my school project.


## Build process

I am proud to say that the python part of this project has no dependencies. No extern libraries are used. For the C part of the project, a basic C compiler shoud do the job, in general, just cloning the project and running the main file with the file to compile being the first commandline argument should be enough. I will probably extend this section when I get to directly compiling a python file to a binary.
