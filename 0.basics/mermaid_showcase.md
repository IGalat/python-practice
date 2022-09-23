# A showcase of Mermaid

[Documentation](https://mermaid-js.github.io/mermaid/#/)

[Online editor](https://mermaid-js.github.io/mermaid-live-editor/)



### Flowchart

```mermaid
flowchart LR
    %% this is a comment
    C[Declared \n before \n arrows]
    A((Start \n circle)) ==Bold\n line==> B[Square]
    A ------> L(Long line \n to rounded)
    B --> C
    C --> part2((Go to \nPart 2))
    L --> in[/input from \n some ext source/]
    in --> if{decision node}
```

```mermaid
flowchart
    start((Patient comes \n to the clinic))
    exists{Registered \n patient}
    a1res{Family doctor \n appointment}
    start -->
    exists--No--> reg[Register] -->
    exists --Yes-->
    a1res --No issue--> finish1((Reassure and \n send home))
    a1res --Skin issue--> finish2(Dermathologist \n appointment)
    a1res -.Heart issue-->
    a2res{Surgeon \n appointment}

    subgraph SIRIUS BUSINESS
        a2res --Critical-->
        op((Operation!))
        a2res --Non-\ncritical--> pills((Pills))
    end
```

### Sequence diagram

```mermaid
sequenceDiagram
    autonumber
    Alice->>John: Hello John, how are you?

    rect rgb(100, 40, 150)
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts!
    end

    John-->>Alice: Great!
    John->>Bob: How about you?

    alt fine
        Bob-->>John: Jolly good!
    else meh
        Bob-->>John: Not so well...
    end
    opt Extra response
        Bob->>John: Thanks for asking
    end
```

### Entity relationship diagram

Value - Meaning

|o	o| -    Zero or one

||	|| -	Exactly one

}o	o{ -	Zero or more (no upper limit)

}|	|{ -	One or more (no upper limit)

```mermaid
erDiagram
    CUSTOMER }|..|{ DELIVERY-ADDRESS : "has 1 or more"
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER ||--o{ INVOICE : "liable for 0 or more"
    DELIVERY-ADDRESS ||--o{ ORDER : receives
    INVOICE ||--|{ ORDER : covers
    ORDER ||--|{ ORDER-ITEM : includes
    PRODUCT-CATEGORY ||--|{ PRODUCT : contains
    PRODUCT ||--o{ ORDER-ITEM : "ordered in"

    CUSTOMER {
        str name
        int age
        bool gender
    }
    PRODUCT {
        int trend
    }
```
