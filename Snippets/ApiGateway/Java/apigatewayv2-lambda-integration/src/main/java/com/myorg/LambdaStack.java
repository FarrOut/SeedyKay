package com.myorg;

import software.amazon.awscdk.NestedStack;
import software.amazon.awscdk.NestedStackProps;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.Function;
import software.amazon.awscdk.services.lambda.Runtime;
import software.constructs.Construct;

public class LambdaStack extends NestedStack {

    public Function function;

    public LambdaStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public LambdaStack(final Construct scope, final String id, final NestedStackProps props) {
        super(scope, id, props);

        function = Function.Builder.create(this, "function").functionName("Lambda-Test").
                runtime(Runtime.PYTHON_3_9).
                code(Code.fromAsset("lambda")).
                handler("event.handler").build();


    }
}
