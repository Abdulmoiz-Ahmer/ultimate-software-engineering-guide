# Singleton Pattern Configuration Challenge

## Problem Statement

Implement a configuration using the singleton pattern with the class `ConfigureVals` with these requirements:

### Class Requirements

- **Constructor** should:

  - Accept properties: `xpoint`, `ypoint`, and `shape`
  - Initialize defaults:
    - `xpoint`: 0
    - `ypoint`: 0
    - `shape`: null
      (when values aren't provided)

- **Singleton Enforcement**:
  - Implement `getConfiguration` method
  - Must return same instance on subsequent calls

### Input/Output Examples

**Sample Input:**

```javascript
getConfiguration({ xpoint: 8, ypoint: 9, shape: "rectangle" }); // First call
getConfiguration({ xpoint: 2, ypoint: 4, shape: "circle" }); // Second call
```

**Sample Output:**

```javascript
ConfigureVals { xpoint: 8, ypoint: 9, shape: 'rectangle' }
ConfigureVals { xpoint: 8, ypoint: 9, shape: 'rectangle' }
```

## Key Observations

- Second call returns same instance as first
- Configuration values from first call persist
- New parameters in subsequent calls are ignored

## Challenge Guidelines

1. Design solution before implementing
2. Focus on singleton enforcement
3. Ensure proper default value handling
4. Try solving independently before checking solutions
