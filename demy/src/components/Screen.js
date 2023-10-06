import { View, StyleSheet } from 'react-native'

const Screen =(props)=>{
    return <View styles={styles.container} children={props.children}/>
}

const styles = StyleSheet.create({
    container:{
        flex: 1,
        backgroundColor: '#fff',
    }
})

export default Screen