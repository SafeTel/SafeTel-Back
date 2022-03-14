##
## EPITECH PROJECT, 2022
## SafeTel-Back
## File description:
## RegexService
##

### LOGIC
# regex import
import re

class RegexCachingService():
    def __init__(self):
        self.__cache = {}


    def GetOrCompileAndCache(self, name: str, pattern: str):
        if (name in self.__cache):
            return self.__cache[name]
        return self.__CompileAndCache(name, pattern)


    def __CompileAndCache(self, name: str, pattern: str):
        compiled = re.compile(pattern)
        self.__cache[name] = compiled
        return compiled
