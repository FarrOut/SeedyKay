package com.myorg;

import org.jetbrains.annotations.Nullable;
import software.amazon.awscdk.Duration;
import software.amazon.awscdk.NestedStackProps;
import software.amazon.awscdk.RemovalPolicy;

import java.util.List;
import java.util.Map;

public class ApiGatewayStackProps implements @Nullable NestedStackProps {
    public String getTargetArn() {
        return targetArn;
    }

    public ApiGatewayStackProps setTargetArn(String targetArn) {
        this.targetArn = targetArn;

        return this;
    }

    private String targetArn;

    @Override
    public @Nullable String getDescription() {
        return NestedStackProps.super.getDescription();
    }

    @Override
    public @Nullable List<String> getNotificationArns() {
        return NestedStackProps.super.getNotificationArns();
    }

    @Override
    public @Nullable Map<String, String> getParameters() {
        return NestedStackProps.super.getParameters();
    }

    @Override
    public @Nullable RemovalPolicy getRemovalPolicy() {
        return NestedStackProps.super.getRemovalPolicy();
    }

    @Override
    public @Nullable Duration getTimeout() {
        return NestedStackProps.super.getTimeout();
    }
}
