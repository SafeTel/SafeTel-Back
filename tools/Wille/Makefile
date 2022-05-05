##
## SAFETEL PROJECT, 2017
## Makefile
## File description:
## repository Makefile
##

SRC	=	main.go

DIR	=	src

NAME	=	wille

all :	$(NAME)

$(NAME):	build run

build-darwin-arch:
	@cd src/; 														\
	GOARCH=amd64 GOOS=darwin go build -o ${NAME}-darwin $(SRC); 	\
	mv ${NAME}-darwin ../${NAME}-darwin;
	@echo "Done: Build-darwin-arch"

build-linux-arch:
	@cd src/; 														\
	GOARCH=amd64 GOOS=linux go build -o ${NAME}-linux $(SRC); 		\
	mv ${NAME}-linux ../${NAME}-linux;
	@echo "Done: Build-linux-arch"

build-windows-arch:
	@cd src/; 														\
	GOARCH=amd64 GOOS=windows go build -o ${NAME}-windows $(SRC); 	\
	mv ${NAME}-windows ../${NAME}-windows;
	@echo "Done: Build-windows-arch"

build:
	@cd src/;					\
	go build -o $(NAME) $(SRC); \
	mv $(NAME) ../$(NAME)
	@echo "Done: Build"


run:
	./${NAME} --help

clean-darwin-arch:	
	@rm ${NAME}-darwin
	@echo "Done: clean-darwin-arch"

clean-linux-arch:	
	@rm ${NAME}-linux
	@echo "Done: clean-linux-arch"

clean-windows-arch:	
	@rm ${NAME}-windows
	@echo "Done: clean-windows-arch"


clean:
	@go clean
	@echo "Done: clean"

fclean:	clean
	@rm $(NAME)
	@echo "Done: fclean"


re: fclean $(NAME)

.PHONY:	clean fclean re