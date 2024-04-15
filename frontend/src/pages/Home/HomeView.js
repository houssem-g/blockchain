import React from 'react'
import PropTypes from 'prop-types'

import NavBar from '../../components/NavBar'

const HomeView = props => {
    const isBrandAdmin = false
    const logoTitle = isBrandAdmin ? 'brands' : 'wallet';

    return (
        <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <NavBar logoTitle={logoTitle} isBrandAdmin={isBrandAdmin} />
        {/* <Footer style={{height: "10%"}} logoTitle={logoTitle} /> */}
        </div>
    )
}

HomeView.propTypes = {title: PropTypes.string.isRequired}

export default HomeView