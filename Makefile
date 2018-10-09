include ./.env

FUNCTION_NAME=$(shell \
	aws cloudformation describe-stacks \
		--profile=$(CLI_PROFILE) \
		--stack-name $(STACK_NAME) \
		--query 'Stacks[0].Outputs[?OutputKey==`FunctionName`].OutputValue' \
		--output text \
)

.PHONY: clean
clean:
	rm -rf package.zip

package.zip: clean
	cd src && zip -r9 package.zip * && mv package.zip ../

.PHONY: update-function
update-function: package.zip
	aws --profile $(CLI_PROFILE) lambda update-function-code \
		--function-name $(FUNCTION_NAME) \
		--zip-file fileb://package.zip
