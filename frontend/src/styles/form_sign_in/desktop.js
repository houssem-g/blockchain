
/* desktop */

import { autocompleteClasses } from "@mui/material"

export const styleFormSignInDesktop = {
    paperStyles: {
        display: 'flex',
        width: '1160px',
        height: '773px',
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        bgcolor: 'background.paper',
        boxShadow: 24,
        p: 4,
    },
    imageForm: {
        width: '580px',
        height: '773px',
        },

    form: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        padding: '0px',
        width: '580px',
        height: '773px',
        background: '#FFFFFF',
        /* Inside auto layout */
        flex: 'none',
        order: 1,
        flexGrow: 0,
    },


    contentBtnClose: {
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'flex-end',
        alignItems: 'center',
        gap: '8px',
        // width: '548px',
        height: '52px',
        marginLeft: 'auto',
        marginRight: "22px",
        /* Inside auto layout */
        flex: 'none',
        order: 0,
        flexGrow: 0,
    },

    btnClose: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        padding: '1px 0px',
        gap: '8px',
        // width: '63px',
        height: '36px',
        // borderRadius: '50px',
        backgroundColor: '#FFFFFF',
        borderStyle: 'none',
        marginTop: '18px',
        /* Inside auto layout */
        flex: 'none',
        order: 0,
        alignSelf: 'stretch',
        flexGrow: 0,
    },

    textClose : {
        width: '43px',
        height: '36px',
        /* text/button */
        fontFamily: 'Inter',
        fontStyle: 'normal',
        fontWeight: '500',
        fontSize: '14px',
        lineHeight: '36px',
        /* identical to box height, or 257% */
        display: 'flex',
        alignItems: 'center',
        textAlign: 'center',
        letterSpacing: '1.25px',
        textTransform: 'capitalize',
        /* custom/primary */
        color: '#111111',
        /* Inside auto layout */
        flex: 'none',
        order: 0,
        flexGrow: 0,
    },

    contentTitle: {
        alignItems: 'center',
        // marginBottom: '24px',
        marginTop: "105px",
        display: 'flex',
        position: 'fixed',
    },

    titleStyles: {
        width: '532px',
        height: '32px',
        
        fontFamily: 'Inter',
        fontStyle: 'normal',
        fontWeight: '500',
        fontSize: '20px',
        lineHeight: '32px',
        /* identical to box height, or 160% */
        textAlign: 'center',
        letterSpacing: '0.25px',
        /* black/0.87 */
        color: 'rgba(0, 0, 0, 0.87)',
        /* Inside auto layout */
        flex: 'none',
        order: 0,
        flexGrow: 1,
    },

    containerStyles: {
        width: '100%',
        display: 'flex',
        flexDirection: 'row',
    },
    contentSubtitle2 : {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        padding: '0px 24px 16px',
        gap: '8px',
        width: '532px',
        height: '60px',
        /* Inside auto layout */
        flex: 'none',
        order: 0,
        alignSelf: 'stretch',
        flexGrow: 0,
    },

    subtitle2: {
        width: '532px',
        height: '44px',
        /* text/subtitle-2 */
        fontFamily: 'Inter',
        fontStyle: 'normal',
        fontWeight: '400',
        fontSize: '14px',
        lineHeight: '22px',
        /* or 157% */
        textAlign: 'center',
        letterSpacing: '0.1px',
        /* black/0.87 */
        color: 'rgba(0, 0, 0, 0.87)',
        /* Inside auto layout */
        flex: 'none',
        order: '0',
        alignSelf: 'stretch',
        flexGrow: '0',
    },

    contentButtonGoogle :{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        padding: '0px 24px',
        gap: '8px',
        width: '532px',
        height: '44px',
        /* Inside auto layout */
        flex: 'none',
        order: 0,
        alignSelf: 'stretch',
        flexGrow: 0,
        marginTop: '0px',
    },

    contentTextOr: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flexStart',
        padding: '0px 24px',
        gap: '8px',
        width: '532px',
        height: '30px',
        /* Inside auto layout */
        flex: 'none',
        order: 4,
        alignSelf: 'stretch',
        flexGrow: 0,
    },

    textOr: {
        width: '532px',
        height: '22px',
        /* text/subtitle-2 */
        fontFamily: 'Inter',
        fontStyle: 'normal',
        fontWeight: '400',
        fontSize: '14px',
        lineHeight: '22px',
        /* identical to box height', or 157% */
        textAlign: 'center',
        letterSpacing: '0.1px', 
        /* black/0.87 */
        color: 'rgba(0, 0, 0, 0.87)',
        /* Inside auto layout */
        flex: 'none',
        order: '0',
        alignSelf: 'stretch',
        flexGrow: '0',
    },

    contentBody : {
        display: 'flex',
        justifyContent: 'space-around',
        height: '420px',
    },

    inputTextContent : {
        height: '290px',
        display: 'flex',
        flexDirection: 'column',
        position: 'initial',
        justifyContent: 'space-around',
    },

    contentName : {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flexStart',
        padding: '0px 24px 16px',
        gap: '8px',
        width: '580px',
        /* Inside auto layout */
        flex: 'none',
        order: 0,
        alignSelf: 'stretch',
        flexGrow: 0,
    },

    inputSignInName: {
        padding: '8px 12px 8px 0px',
        /* size: 'default', */
        height: '56px',
        width: '532px',
        /* left: '24px', */
        top: '0px',
        borderRadius: '4px',

    },

    contentEmail : {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flexStart',
        padding: '0px 24px 16px',
        gap: '8px',
        width: '580px',
        /* Inside auto layout */
        flex: 'none',
        order: 0,
        alignSelf: 'stretch',
        flexGrow: 0,
    },

    inputSignInEmail: {
        padding: '8px 12px 8px 0px',
        /* size: 'default', */
        height: '56px',
        width: '532px',
        /* left: '24px', */
        borderRadius: '4px',
    },

    contentPwd : {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flexStart',
        padding: '0px 24px 4px',
        gap: '8px',
        width: '580px',
        /* Inside auto layout */
        flex: 'none',
        order: 0,
        alignSelf: 'stretch',
        flexGrow: 0,
    },

    inputSignInPwd: {
        padding: '8px 12px 8px 0px',
        /* size: 'default', */
        height: '56px',
        width: '532px',
        /* left: '24px', */
        borderRadius: '4px',
    },

    forgetPwd: {
        /* Forgot password? */
        width: '532px',
        height: '22px',
        fontFamily: 'Inter',
        fontStyle: 'normal',
        fontWeight: '400',
        fontSize: '15px',
        lineHeight: '22px',
        /* identical to box height', or 157% */
        letterSpacing: '0.1px',
        textDecorationLine: 'underline',
        /* black/0.87 */
        color: 'rgba(0, 0, 0, 0.87)',
        /* Inside auto layout */
        flex: 'none',
        alignSelf: 'stretch',
        flexGrow: '0',
    },

    emailError: {
        color: 'red',
        fontSize: '14px'
    },

    contentButtonLogin: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flexStart',
        padding: '0px 24px 16px',
        gap: '8px',
        width: '580px',
        height: '90px',
        marginTop: '-10px !important',
        /* Inside auto layout */
        flex: 'none',
        order: 0,
        alignSelf: 'stretch',
        flexGrow: 0,
    },

    buttonLogin: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        padding: '0px 0px',
        gap: '16px',
        width: '105px',
        height: '44px',
        /* custom/primary */
        background: '#111111',
        borderRadius: '50px',
        /* Inside auto layout */
        flex: 'none',
        order: 0,
        flexGrow: 0,
    },

    texthaveAccount: {
        /* Already have an account? Log in */
        width: '532px',
        height: '22px',
        fontFamily: 'Inter',
        fontStyle: 'normal',
        fontWeight: '400',
        fontSize: '14px',
        lineHeight: '22px',
        /* identical to box height', or 157% */
        letterSpacing: '0.1px',
        textDecorationLine: 'underline',
        /* black/0.87 */
        color: 'rgba(0, 0, 0, 0.87)',
        /* Inside auto layout */
        flex: 'none',
        order: '1',
        alignSelf: 'stretch',
        flexGrow: '0',
    },



}
// /* mobile */
// @media (max-width: 900px) {
//     .form {
//         display: flex,
//         flex-direction: column,
//         align-items: center,
//         padding: 0px,

//         width: 375px,
//         height: 578px,

//         background: #FFFFFF,

//         /* Inside auto layout */
//         flex: none,
//         align-self: stretch,
//         flex-grow: 0,
//     }

//     .containerImageStyles {
//         margin-left: auto,
//         margin-right: auto,
//         width: 20em,
//         flex-direction: column,
//     }
//     .imageForm {
//         height: 403px,
        
//     }

//     .inputSignIn {
//         width: 327px,
//         height: 22px,

//         /* text/subtitle-2 */
//         font-family: 'Inter',
//         font-style: normal,
//         font-weight: 400,
//         font-size: 14px,
//         line-height: 22px,

//         /* identical to box height, or 157% */
//         text-align: center,
//         letter-spacing: 0.1px,

//         /* black/0.87 */
//         color: rgba(0, 0, 0, 0.87),


//         /* Inside auto layout */
//         flex: none,
//         align-self: stretch,
//         flex-grow: 0,

//     }
//     .contentLogin {

//         /* Auto layout */
//         /* display: flex,
//         flex-direction: column,
//         align-items: flex-start,
//         padding: 0px 24px 16px,
//         gap: 8px,

//         width: 375px,
//         height: 90px,


//         /* Inside auto layout */
//         /* flex: none,
//         order: 7,
//         align-self: stretch,
//         flex-grow: 0, */
//     }
//     .forgetPwd {
//         /* Forgot password? */

//         width: 327px,
//         height: 22px,

//         font-family: 'Inter',
//         font-style: normal,
//         font-weight: 400,
//         font-size: 14px,
//         line-height: 22px,

//         /* identical to box height, or 157% */
//         letter-spacing: 0.1px,
//         text-decoration-line: underline,

//         /* black/0.87 */
//         color: rgba(0, 0, 0, 0.87),


//         /* Inside auto layout */
//         flex: none,
//         align-self: stretch,
//         flex-grow: 0,
//     }
//     .subtitle2 {
//         width: 327px,
//         height: 44px,
        
//         /* text/subtitle-2 */
//         font-family: 'Inter',
//         font-style: normal,
//         font-weight: 400,
//         font-size: 14px,
//         line-height: 22px,
        
//         /* or 157% */
//         text-align: center,
//         letter-spacing: 0.1px,
        
//         /* black/0.87 */
//         color: rgba(0, 0, 0, 0.87),
        
        
//         /* Inside auto layout */
//         flex: none,
//         align-self: stretch,
//         flex-grow: 0,

        
//     }
//     .texthaveAccount {
//         width: 327px,
//         height: 22px,
//         margin-top: 2px !important,

//         font-family: 'Inter',
//         font-style: normal,
//         font-weight: 400,
//         font-size: 14px,
//         line-height: 22px,

//         /* identical to box height, or 157% */
//         letter-spacing: 0.1px,
//         text-decoration-line: underline,

//         /* black/0.87 */
//         color: rgba(0, 0, 0, 0.87),


//         /* Inside auto layout */
//         flex: none,

//         align-self: stretch,
//         flex-grow: 0,
//     }

//     .textOr  {
//         width: 327px,
//         height: 22px,

//         /* text/subtitle-2 */
//         font-family: 'Inter',
//         font-style: normal,
//         font-weight: 400,
//         font-size: 14px,
//         line-height: 22px,
//         /* identical to box height, or 157% */
//         text-align: center,
//         /* black/0.87 */
//         color: rgba(0, 0, 0, 0.87),
//         /* Inside auto layout */
//         align-self: stretch,

//     }
//     .buttonLogin {
//         display: flex,
//         flex-direction: row,
//         align-items: center,
//         padding: 0px 16px,
//         gap: 16px,

//         height: 44px,

//         /* custom/primary */
//         background: #111111,
//         border-radius: 50px,

//         /* Inside auto layout */
//         flex: none,

//         flex-grow: 0,
//     }


// }

