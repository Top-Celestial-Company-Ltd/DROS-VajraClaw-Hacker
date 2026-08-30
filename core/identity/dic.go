package identity

type Subject struct {
    ID     string `json:"id"`
    Issuer string `json:"issuer"`
}

type Agent struct {
    ID      string `json:"id"`
    Version string `json:"version"`
}

type Session struct {
    ID        string `json:"id"`
    CreatedAt int64  `json:"created_at"`
}

type Delegation struct {
    AllowedBy string `json:"allowed_by"`
    Scope     string `json:"scope"`
}

// DROSIdentityContext represents the Layer A Human/Agent Context.
type DROSIdentityContext struct {
    Subject    Subject    `json:"subject"`
    Agent      Agent      `json:"agent"`
    Session    Session    `json:"session"`
    Delegation Delegation `json:"delegation"`
}
